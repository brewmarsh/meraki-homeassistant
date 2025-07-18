import asyncio
import json
import logging
import random
import ssl
import sys
import time
import urllib.parse
from datetime import datetime

import aiohttp
from meraki.__init__ import __version__
from meraki.aio.rest_session import AsyncRestSession
from meraki.config import *
from meraki.exceptions import *
from meraki.rest_session import user_agent_extended


class PatchedAsyncRestSession(AsyncRestSession):
    async def _request(self, metadata, method, url, **kwargs):
        # Metadata on endpoint
        tag = metadata["tags"][0]
        operation = metadata["operation"]

        # Update request kwargs with session defaults
        if self._certificate_path:
            kwargs.setdefault("ssl", self._sslcontext)
        if self._requests_proxy:
            kwargs.setdefault("proxy", self._requests_proxy)
        kwargs.setdefault("timeout", self._single_request_timeout)

        # Ensure proper base URL
        allowed_domains = ['meraki.com', 'meraki.cn']
        parsed_url = urllib.parse.urlparse(url)

        if any(domain in parsed_url.netloc for domain in allowed_domains):
            abs_url = url
        else:
            abs_url = self._base_url + url

        # Set maximum number of retries
        retries = self._maximum_retries

        # Option to simulate non-safe API calls without actually sending them
        if self._logger:
            self._logger.debug(metadata)
        if self._simulate and method != "GET":
            if self._logger:
                self._logger.info(f"{tag}, {operation} > {abs_url} - SIMULATED")
            return None
        else:
            response = None
            message = None
            message_is_dict = False
            for _ in range(retries):
                # Make sure that the response object gets closed during retries
                if response:
                    response.release()
                    response = None

                # Make the HTTP request to the API endpoint
                try:
                    if self._logger:
                        self._logger.info(f"{method} {abs_url}")
                    response = await self._req_session.request(
                        method, abs_url, **kwargs
                    )
                    reason = response.reason if response.reason else None
                    status = response.status
                except Exception as e:
                    if self._logger:
                        self._logger.warning(
                            f"{tag}, {operation} > {abs_url} - {e}, retrying in 1 second"
                        )
                    await asyncio.sleep(1)
                    continue

                if 200 <= status < 300:
                    if "page" in metadata:
                        counter = metadata["page"]
                        if self._logger:
                            self._logger.info(
                                f"{tag}, {operation}; page {counter} > {abs_url} - {status} {reason}"
                            )
                    else:
                        if self._logger:
                            self._logger.info(
                                f"{tag}, {operation} > {abs_url} - {status} {reason}"
                            )
                    # For non-empty response to GET, ensure valid JSON
                    try:
                        if method == "GET":
                            await response.json(content_type = None)
                        return response
                    except (
                            json.decoder.JSONDecodeError,
                            aiohttp.client_exceptions.ContentTypeError,
                    ) as e:
                        if self._logger:
                            self._logger.warning(
                                f"{tag}, {operation} > {abs_url} - {e}, retrying in 1 second"
                            )
                        await asyncio.sleep(1)
                # Handle 3XX redirects automatically
                elif 300 <= status < 400:
                    abs_url = response.headers["Location"]
                    substring = "meraki.com/api/v"
                    if substring not in abs_url:
                        substring = "meraki.cn/api/v"
                    self._base_url = abs_url[
                                     : abs_url.find(substring) + len(substring) + 1
                                     ]
                # Rate limit 429 errors
                elif status == 429:
                    if "Retry-After" in response.headers:
                        wait = int(response.headers["Retry-After"])
                    else:
                        wait = random.randint(1, self._nginx_429_retry_wait_time)
                    if self._logger:
                        self._logger.warning(
                            f"{tag}, {operation} > {abs_url} - {status} {reason}, retrying in {wait} seconds"
                        )
                    await asyncio.sleep(wait)
                # 5XX errors
                elif status >= 500:
                    if self._logger:
                        self._logger.warning(
                            f"{tag}, {operation} > {abs_url} - {status} {reason}, retrying in 1 second"
                        )
                    await asyncio.sleep(1)
                # 4XX errors
                else:
                    try:
                        message = await response.json(content_type = None)
                        message_is_dict = True
                    except aiohttp.client_exceptions.ContentTypeError:
                        try:
                            message = (await response.text())[:100]
                            message_is_dict = True
                        except:
                            message = None
                            message_is_dict = False

                    # Check for specific concurrency errors
                    network_delete_concurrency_error_text = 'This may be due to concurrent requests to delete networks.'
                    action_batch_concurrency_error = {'errors': [
                        'Too many concurrently executing batches. Maximum is 5 confirmed but not yet executed batches.']
                    }
                    # Check specifically for network delete concurrency error
                    if message_is_dict and 'errors' in message.keys() \
                            and network_delete_concurrency_error_text in message['errors'][0]:
                        wait = random.randint(15, self._network_delete_retry_wait_time)
                        if self._logger:
                            self._logger.warning(f'{tag}, {operation} - {status} {reason}, retrying in {wait} seconds')
                        time.sleep(wait)
                        retries -= 1
                        if retries == 0:
                            raise APIError(metadata, response)
                    # Check specifically for action batch concurrency error
                    if message == action_batch_concurrency_error:
                        wait = self._action_batch_retry_wait_time
                        if self._logger:
                            self._logger.warning(
                                f"{tag}, {operation} > {abs_url} - {status} {reason}, retrying in {wait} seconds"
                            )
                        await asyncio.sleep(wait)

                    elif self._retry_4xx_error:
                        wait = random.randint(1, self._retry_4xx_error_wait_time)
                        if self._logger:
                            self._logger.warning(
                                f"{tag}, {operation} > {abs_url} - {status} {reason}, retrying in {wait} seconds"
                            )
                        await asyncio.sleep(wait)

                    # All other client-side errors
                    else:
                        if self._logger:
                            self._logger.error(
                                f"{tag}, {operation} > {abs_url} - {status} {reason}, {message}"
                            )
                        raise AsyncAPIError(metadata, response, message)
            raise AsyncAPIError(
                metadata, response, "Reached retry limit: " + str(message)
            )
