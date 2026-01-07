# Meraki Camera Component Architecture

## Implementation Plan

The implementation will follow a three-phase approach to ensure a controlled and verifiable re-integration of the camera functionality.

### Phase 1: Code Re-integration

1. **Update the `MVHandler`:**

   - Open `custom_components/meraki_ha/discovery/handlers/mv.py`.
   - Add the necessary import for the `MerakiCamera` class at the top of the file:

     ```python
     from ...camera import MerakiCamera
     ```

   - Within the `MVHandler`'s `__init__` method, ensure that `camera_service` is correctly passed and stored as an attribute (`self._camera_service`).
   - Inside the `discover_entities` method, add the code to instantiate and append the `MerakiCamera` entity to the list of entities to be returned. This should be the first entity appended, as it is the primary entity for a camera device.

     ```python
     # Always create the base camera entity
     entities.append(
         MerakiCamera(
             self._coordinator,
             self.device,
             self._camera_service,
         )
     )
     ```

2. **Review the `DeviceDiscoveryService`:**
   - Open `custom_components/meraki_ha/discovery/service.py`.
   - Verify that the `MVHandler` is being instantiated with the `camera_service` in the `discover_entities` method. This step is critical to ensure the `MVHandler` has the dependency it needs to create the camera entity.

### Phase 2: Test Suite Refinement

1. **Update the `MVHandler` Tests:**

   - Open `tests/discovery/handlers/test_mv.py`.
   - Modify the `test_mv_handler_all_features` test case.
   - Add a new assertion to the test to explicitly check for the presence of a `MerakiCamera` instance in the list of returned entities.

     ```python
     assert any(isinstance(e, MerakiCamera) for e in entities)
     ```

   - Ensure all other existing test cases are updated to also include this assertion, as a `MerakiCamera` entity should now always be discovered for an MV device.

### Phase 3: Validation and Finalization

1. **Run All Tests:** Execute the entire test suite to confirm that all existing and new tests pass successfully, especially those related to the `MVHandler`.
2. **Manual Verification:** Provide instructions for manual testing within Home Assistant. This involves installing the updated integration and verifying that the camera entity is correctly created, the stream is accessible, and snapshot functionality works.
3. **Code Cleanup:** Once validated, remove any temporary or legacy code from the refactor and finalize the file with clear comments and docstrings.
