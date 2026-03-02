"""JavaScript templates for Meraki Web UI E2E testing."""

JS_TEMPLATE = """
// Initialize calls storage if not exists
if (!sessionStorage.getItem('mockCallWS')) {{
    sessionStorage.setItem('mockCallWS', JSON.stringify([]));
}}

// Define mock HA elements
{ha_elements_js}

document.addEventListener('DOMContentLoaded', () => {{
    const panel = document.createElement('meraki-panel');
    document.body.appendChild(panel);
    panel.panel = {{
        config: {{
            config_entry_id: 'test-entry-id-from-panel'
        }}
    }};
    panel.hass = {{
        states: {{
            "switch.office_switch": {{ state: "on", attributes: {{}} }},
            "camera.front_door_camera": {{
                state: "idle",
                attributes: {{}}
            }},
            "switch.guest_wifi": {{ state: "on", attributes: {{}} }}
        }},
        callWS: async (msg) => {{
            console.log("callWS called with type: " + msg.type);

            // Store in sessionStorage to persist across reloads
            const calls = JSON.parse(
                sessionStorage.getItem('mockCallWS') || '[]'
            );
            calls.push(msg);
            sessionStorage.setItem('mockCallWS', JSON.stringify(calls));

            if (msg.type === 'meraki_ha/get_config') {{
                return {mock_data_json};
            }}
            if (msg.type === 'meraki_ha/update_options') {{
                return {{}};
            }}
             if (msg.type === 'call_service') {{
                return {{}};
            }}
            return {{}};
        }},
        callService: async (domain, service, data) => {{
             console.log(`callService: ${{domain}}.${{service}}`, data);
              const calls = JSON.parse(
                sessionStorage.getItem('mockCallWS') || '[]'
            );
            calls.push({{
                type: 'call_service',
                domain,
                service,
                service_data: data
            }});
            sessionStorage.setItem('mockCallWS', JSON.stringify(calls));
        }}
    }};
}});
"""

HA_ELEMENTS_JS = """
class HACard extends HTMLElement {
    constructor() { super(); this.attachShadow({mode: 'open'}); }
    connectedCallback() {
        this.shadowRoot.innerHTML = `
            <div style="
                border: 1px solid #ccc;
                padding: 16px;
                display: block;">
                <slot></slot>
            </div>
        `;
        this.style.display = 'block';
    }
}
class HAIcon extends HTMLElement {
    constructor() { super(); this.attachShadow({mode: 'open'}); }
    connectedCallback() {
        const icon = this.getAttribute('icon');
        this.shadowRoot.innerHTML = `
            <span style="display: flex; align-items: center;
                         justify-content: center;">
                icon: ${icon}
            </span>
        `;
        this.style.display = 'inline-block';
        this.style.width = '24px';
        this.style.height = '24px';
    }
    static get observedAttributes() { return ['icon']; }
    attributeChangedCallback(name, oldValue, newValue) {
        if (name === 'icon') {
            this.shadowRoot.innerHTML = `
                <span style="display: flex; align-items: center;
                             justify-content: center;">
                    icon: ${newValue}
                </span>
            `;
        }
    }
}
class HASwitch extends HTMLElement {
    constructor() { super(); this.attachShadow({mode: 'open'}); }
    connectedCallback() {
        this.shadowRoot.innerHTML = `<input type="checkbox" />`;
        this.style.display = 'inline-block';
        const input = this.shadowRoot.querySelector('input');
        input.checked = this.hasAttribute('checked');
        input.addEventListener('change', (e) => {
           this.dispatchEvent(new CustomEvent('change', {
               detail: { value: e.target.checked },
               bubbles: true,
               composed: true
           }));
        });
    }
    set checked(val) {
        const input = this.shadowRoot.querySelector('input');
        if (input) input.checked = val;
        if (val) this.setAttribute('checked', '');
        else this.removeAttribute('checked');
    }
    get checked() {
        const input = this.shadowRoot.querySelector('input');
        return input ? input.checked : false;
    }
    click() {
        const input = this.shadowRoot.querySelector('input');
        if (input) {
            input.click();
        }
    }
}

if (!customElements.get('ha-card')) {
    customElements.define('ha-card', HACard);
}
if (!customElements.get('ha-icon')) {
    customElements.define('ha-icon', HAIcon);
}
if (!customElements.get('ha-switch')) {
    customElements.define('ha-switch', HASwitch);
}
"""
