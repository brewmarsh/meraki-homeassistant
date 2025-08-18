console.log("Meraki HA Web UI Simulated App v4 (Correct Routing) Loaded");

// --- Helper: Create DOM element ---
function h(tag, classList = [], children = []) {
    const el = document.createElement(tag);
    if (classList.length) el.className = classList.join(' ');

    if (!Array.isArray(children)) {
        children = [children];
    }

    children.forEach(child => {
        if (typeof child === 'string') {
            el.appendChild(document.createTextNode(child));
        } else if (child) {
            el.appendChild(child);
        }
    });
    return el;
}

// --- Layout Components ---
function createSidebar(pathname) {
    const navigation = [
        { name: 'Dashboard', href: '/' },
        { name: 'Networks', href: '/networks' },
        { name: 'Clients', href: '/clients' },
        { name: 'Settings', href: '/settings' },
    ];
    const navItems = navigation.map(item => {
        const link = h('a', ['flex', 'items-center', 'px-4', 'py-2', 'text-sm', 'font-medium', 'rounded-md', 'transition-colors', 'hover:bg-light-background', 'dark:hover:bg-dark-card'], [item.name]);
        link.href = item.href;
        return link;
    });
    return h('div', ['flex', 'flex-col', 'h-full', 'bg-light-card', 'dark:bg-dark-card', 'border-r', 'border-light-border', 'dark:border-dark-border'], [
        h('div', ['flex', 'items-center', 'justify-center', 'h-16', 'border-b', 'border-light-border', 'dark:border-dark-border'], [h('h1', ['text-xl', 'font-bold'], 'Meraki UI')]),
        h('nav', ['flex-1', 'p-4', 'space-y-2'], navItems)
    ]);
}

function createHeader(title) {
    return h('header', ['bg-light-card', 'dark:bg-dark-card', 'shadow-sm', 'border-b', 'border-light-border', 'dark:border-dark-border'], [
        h('div', ['max-w-7xl', 'mx-auto', 'py-4', 'px-4', 'sm:px-6', 'lg:px-8'], [h('h1', ['text-lg', 'font-semibold'], title)])
    ]);
}

// --- Page Renderers ---
async function renderDashboard(contentEl) {
    try {
        const [networksRes, clientsRes] = await Promise.all([fetch('/api/networks'), fetch('/api/clients')]);
        if (!networksRes.ok || !clientsRes.ok) throw new Error('Failed to fetch data');
        const networks = await networksRes.json();
        const clients = await clientsRes.json();

        const grid = h('div', ['grid', 'grid-cols-1', 'md:grid-cols-2', 'gap-6']);
        const networkItems = networks.map(n => {
            const link = h('a', ['block', 'hover:bg-light-background', 'dark:hover:bg-dark-background'], [h('div', ['py-4', 'px-6'], [h('p', ['font-medium', 'text-cisco-blue', 'truncate'], n.name), h('p', ['text-sm', 'text-gray-500', 'dark:text-gray-400'], `ID: ${n.id}`)])]);
            link.href = `/networks/${n.id}`;
            return link;
        });
        const clientItems = clients.map(c => {
            const link = h('a', ['block', 'hover:bg-light-background', 'dark:hover:bg-dark-background'], [h('div', ['py-4', 'px-6'], [h('p', ['font-medium', 'text-cisco-blue', 'truncate'], c.description || 'No description'), h('p', ['text-sm', 'text-gray-500', 'dark:text-gray-400'], `MAC: ${c.mac}`)])]);
            link.href = `/clients/${c.mac}`;
            return link;
        });
        const networkCard = h('div', ['bg-light-card', 'dark:bg-dark-card', 'shadow', 'rounded-lg'], [h('div', ['p-6'], [h('h2', ['text-xl', 'font-semibold'], `Networks (${networks.length})`)]), h('div', ['divide-y', 'divide-light-border', 'dark:divide-dark-border'], networkItems)]);
        const clientCard = h('div', ['bg-light-card', 'dark:bg-dark-card', 'shadow', 'rounded-lg'], [h('div', ['p-6'], [h('h2', ['text-xl', 'font-semibold'], `Clients (${clients.length})`)]), h('div', ['divide-y', 'divide-light-border', 'dark:divide-dark-border'], clientItems)]);
        grid.appendChild(networkCard);
        grid.appendChild(clientCard);
        contentEl.innerHTML = '';
        contentEl.appendChild(grid);
    } catch (e) {
        contentEl.innerHTML = `<p class="text-center text-red-500">Error: ${e.message}</p>`;
    }
}

async function renderDetailPage(contentEl, type, id) {
    try {
        const res = await fetch(`/api/${type}/${id}`);
        if (!res.ok) throw new Error(`Failed to fetch ${type} detail`);
        const data = await res.json();
        const backLink = h('a', ['text-cisco-blue', 'hover:underline'], '← Back to Dashboard');
        backLink.href = '/';
        const header = h('div', ['px-4', 'py-5', 'sm:px-6', 'border-b', 'border-light-border', 'dark:border-dark-border'], [h('h3', ['text-lg', 'leading-6', 'font-medium'], `${type === 'networks' ? 'Network' : 'Client'} Information`), h('p', ['mt-1', 'max-w-2xl', 'text-sm', 'text-gray-500', 'dark:text-gray-400'], `Details for ${data.name || data.description || data.mac}`)]);
        const dl = h('dl');
        Object.entries(data).forEach(([key, value], index) => {
            const item = h('div', [`${index % 2 === 0 ? 'bg-light-card dark:bg-dark-card' : 'bg-light-background dark:bg-dark-background'}`, 'px-4', 'py-5', 'sm:grid', 'sm:grid-cols-3', 'sm:gap-4', 'sm:px-6'], [h('dt', ['text-sm', 'font-medium', 'text-gray-500', 'dark:text-gray-400', 'capitalize'], key), h('dd', ['mt-1', 'text-sm', 'sm:mt-0', 'sm:col-span-2'], JSON.stringify(value, null, 2))]);
            dl.appendChild(item);
        });
        const detailCard = h('div', ['bg-light-card', 'dark:bg-dark-card', 'shadow', 'overflow-hidden', 'sm:rounded-lg'], [header, h('div', ['border-t', 'border-light-border', 'dark:border-dark-border'], [dl])]);
        contentEl.innerHTML = '';
        contentEl.appendChild(h('div', ['mb-4'], [backLink]));
        contentEl.appendChild(detailCard);
    } catch (e) {
        contentEl.innerHTML = `<p class="text-center text-red-500">Error: ${e.message}</p>`;
    }
}

// --- Main Router ---
function getTitle(pathname) {
    const networkMatch = pathname.match(/^\/networks\/([^/]+)/);
    if (networkMatch) return 'Network Detail';

    const clientMatch = pathname.match(/^\/clients\/([^/]+)/);
    if (clientMatch) return 'Client Detail';

    switch (pathname) {
        case '/': return 'Dashboard';
        case '/networks': return 'Networks';
        case '/clients': return 'Clients';
        case '/settings': return 'Settings';
        default: return 'Dashboard';
    }
}

function router() {
    const root = document.getElementById('root');
    const pathname = window.location.pathname;
    const title = getTitle(pathname);
    root.innerHTML = '';
    const sidebarContainer = h('div', ['w-64', 'flex-shrink-0']);
    sidebarContainer.appendChild(createSidebar(pathname));
    const mainContentContainer = h('div', ['flex-1', 'flex', 'flex-col', 'overflow-hidden']);
    const header = createHeader(title);
    const main = h('main', ['flex-1', 'overflow-y-auto']);
    const contentWrapper = h('div', ['py-6']);
    const contentEl = h('div', ['max-w-7xl', 'mx-auto', 'px-4', 'sm:px-6', 'lg:px-8']);
    contentEl.id = 'page-content';
    contentEl.textContent = 'Loading...';
    contentWrapper.appendChild(contentEl);
    main.appendChild(contentWrapper);
    mainContentContainer.appendChild(header);
    mainContentContainer.appendChild(main);
    const mainLayout = h('div', ['flex', 'h-screen', 'text-light-text', 'dark:text-dark-text'], [sidebarContainer, mainContentContainer]);
    root.appendChild(mainLayout);

    const networkMatch = pathname.match(/^\/networks\/([^/]+)/);
    if (networkMatch) {
        renderDetailPage(contentEl, 'networks', networkMatch[1]);
        return;
    }
    const clientMatch = pathname.match(/^\/clients\/([^/]+)/);
    if (clientMatch) {
        renderDetailPage(contentEl, 'clients', clientMatch[1]);
        return;
    }
    renderDashboard(contentEl);
}

document.addEventListener('DOMContentLoaded', router);
