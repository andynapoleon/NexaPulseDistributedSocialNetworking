import { readable } from "svelte/store";

// color design tokens export
export const colorTokens = readable({
  // shades of grey
  grey: {
    0: "#FFFFFF",
    10: "#F6F6F6",
    50: "#F0F0F0",
    100: "#E0E0E0",
    200: "#C2C2C2",
    300: "#A3A3A3",
    400: "#858585",
    500: "#666666",
    600: "#4D4D4D",
    700: "#333333",
    800: "#1A1A1A",
    900: "#0A0A0A",
    1000: "#000000",
  },
  // shades of teal
  primary: {
    50: "#d5fbf3",
    100: "#7efbe1",
    200: "#29e1cb",
    300: "#1dc2ae",
    400: "#00a398",
    500: "#008480",
    600: "#0f6460",
    700: "#0b4b3f",
    800: "#123131",
    900: "#111818",
  },
});
