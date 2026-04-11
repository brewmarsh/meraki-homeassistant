export interface CustomCard {
  type: string;
  name: string;
  description: string;
  preview: boolean;
  version?: string;
}

declare global {
  interface Window {
    customCards: CustomCard[];
  }
}
