import React from 'react';

interface NetworkViewProps {
    activeView: { view: string; networkId?: string };
    setActiveView: (view: { view:string; deviceId?: string, networkId?: string }) => void;
    data: any;
}

const NetworkView: React.FC<NetworkViewProps> = ({ activeView, setActiveView, data }) => {
    const network = data.networks.find((n: any) => n.id === activeView.networkId);

    if (!network) {
        return <div>Network not found</div>;
    }

    return (
        <div>
            <button onClick={() => setActiveView({ view: 'dashboard' })} className="mb-4">
                &larr; Back to Dashboard
            </button>
            <h2 className="text-xl font-semibold mb-4">Network Information</h2>
            <p>Name: {network.name}</p>
            <p>ID: {network.id}</p>
            <p>Product Types: {network.product_types.join(', ')}</p>
        </div>
    );
};

export default NetworkView;
