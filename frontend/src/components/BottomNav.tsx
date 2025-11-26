import type { FC } from "react";

type BottomNavProps = {
  onMenuToggle: () => void;
};

const BottomNav: FC<BottomNavProps> = ({ onMenuToggle }) => {
  return (
    <nav className="bottom-nav" aria-label="Mobile shortcuts">
      <button className="bottom-nav__item" type="button" onClick={onMenuToggle}>
        <span className="icon">☰</span>
        <span>Menu</span>
      </button>
      <button className="bottom-nav__item" type="button">
        <span className="icon">★</span>
        <span>Starred</span>
      </button>
      <button className="bottom-nav__item" type="button">
        <span className="icon">➕</span>
        <span>New</span>
      </button>
      <button className="bottom-nav__item" type="button">
        <span className="icon">🔔</span>
        <span>Alerts</span>
      </button>
    </nav>
  );
};

export default BottomNav;
