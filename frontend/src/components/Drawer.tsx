import { clsx } from "clsx";
import type { FC, ReactNode } from "react";

type DrawerProps = {
  open: boolean;
  onClose: () => void;
  children: ReactNode;
};

const Drawer: FC<DrawerProps> = ({ open, onClose, children }) => {
  return (
    <div className={clsx("drawer", open && "drawer--open")}>
      <div className="drawer__backdrop" aria-hidden={!open} onClick={onClose} />
      <div className="drawer__panel" role="dialog" aria-modal="true" aria-label="Navigation">
        <div className="drawer__handle" onClick={onClose}>
          <span className="icon">×</span>
          <span className="drawer__hint">Swipe left or tap to close</span>
        </div>
        {children}
      </div>
    </div>
  );
};

export default Drawer;
