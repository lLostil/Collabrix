import type { FC } from "react";

type TopBarProps = {
  onMenuToggle: () => void;
  isDrawerOpen: boolean;
};

const TopBar: FC<TopBarProps> = ({ onMenuToggle, isDrawerOpen }) => {
  return (
    <header className="topbar">
      <div className="topbar__left">
        <button
          className="icon-button"
          aria-label={isDrawerOpen ? "Close navigation" : "Open navigation"}
          aria-expanded={isDrawerOpen}
          aria-controls="sidebar"
          onClick={onMenuToggle}
        >
          <span className="icon">☰</span>
        </button>
        <div>
          <div className="topbar__title">Collabrix</div>
          <div className="topbar__subtitle">Keep your team aligned from any device</div>
        </div>
      </div>
      <div className="topbar__actions">
        <button className="ghost-button" type="button">
          Search
        </button>
        <button className="primary-button" type="button">
          New
        </button>
      </div>
    </header>
  );
};

export default TopBar;
