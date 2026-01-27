import React, { useEffect, useRef } from 'react';

interface HaSwitchProps {
  checked?: boolean;
  disabled?: boolean;
  onChange?: (checked: boolean) => void;
  className?: string;
  style?: React.CSSProperties;
}

const HaSwitch: React.FC<HaSwitchProps> = ({
  checked,
  disabled,
  onChange,
  className,
  style,
}) => {
  const ref = useRef<HTMLElement>(null);

  useEffect(() => {
    const element = ref.current;
    if (!element || !onChange) return;

    const handleChange = (e: Event) => {
      e.stopPropagation();
      // Cast to any to access 'checked' property of the custom element
      onChange((e.target as any).checked);
    };

    element.addEventListener('change', handleChange);
    return () => {
      element.removeEventListener('change', handleChange);
    };
  }, [onChange]);

  return (
    <ha-switch
      ref={ref}
      checked={checked}
      disabled={disabled}
      className={className}
      style={style}
    ></ha-switch>
  );
};

export default HaSwitch;
