# Collabrix frontend

Responsive React UI tailored for desktop, tablet, and mobile layouts. Built with Vite + TypeScript.

## Scripts

- `npm install`
- `npm run dev` — start the dev server on port 5173
- `npm run build` — type-check and create a production build
- `npm run preview` — preview the production build

## Layout behavior

- **Desktop (≥ 1025px)**: persistent sidebar next to the main content with wide cards and stat panels.
- **Tablet (769–1024px)**: sidebar moves into a slide-in drawer triggered by the top hamburger; content stacks vertically.
- **Mobile (≤ 768px)**: top bar keeps the menu toggle, drawer supports swipe-to-open/close, and a sticky bottom navigation surfaces key actions.
- **Small phones (≤ 540px)**: tighter padding, rounded surfaces, and slightly reduced heading sizes to keep text readable while preserving touchable tap targets.

## Interaction cues

- Drawer can be opened via hamburger or a left-edge swipe; close via swipe or tapping the backdrop.
- Buttons and pills maintain 44px+ hit areas for touch.
