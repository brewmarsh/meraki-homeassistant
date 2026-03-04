import { useState, useEffect, RefObject } from 'react';
import { HaTabsElement } from '../types/ha-frontend';

export const useHaTabs = (tabsRef: RefObject<HaTabsElement>, loading: boolean, initialTab: string = 'networks') => {
  const [activeTab, setActiveTab] = useState(initialTab);
  const [activeView, setActiveView] = useState<{ view: string; deviceId?: string }>({
    view: 'dashboard',
    deviceId: undefined,
  });

  useEffect(() => {
    const tabs = tabsRef.current;
    if (tabs && !loading) {
      const handleSelectEvent = (e: Event | CustomEvent) => {
        const target = e.target as HaTabsElement;
        const detail = (e as CustomEvent).detail;
        const newTab = target?.selected || detail?.selected;
        if (newTab) {
          setActiveTab(newTab);
          setActiveView({ view: 'dashboard' });
        }
      };
      tabs.addEventListener('iron-select', handleSelectEvent as EventListener);
      tabs.addEventListener('select', handleSelectEvent as EventListener);
      return () => {
        tabs.removeEventListener('iron-select', handleSelectEvent as EventListener);
        tabs.removeEventListener('select', handleSelectEvent as EventListener);
      };
    }
  }, [tabsRef, loading]);

  return { activeTab, setActiveTab, activeView, setActiveView };
};
