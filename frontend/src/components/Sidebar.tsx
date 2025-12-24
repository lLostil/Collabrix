import { clsx } from "clsx";
import type { FC } from "react";

const links = [
  { label: "Spaces", description: "Browse and manage workspaces" },
  { label: "Pages", description: "Recent and pinned pages" },
  { label: "Tasks", description: "Tasks assigned to you" },
  { label: "Comments", description: "Mentions & inline notes" },
  { label: "Settings", description: "Notifications & profile" },
];

export type SidebarProps = {
  collapsed?: boolean;
  className?: string;
};

const Sidebar: FC<SidebarProps> = ({ collapsed = false, className }) => {
  return (
    <aside
      className={clsx(
        "sidebar",
        collapsed && "sidebar--collapsed",
        className,
      )}
    >
      <div className="sidebar__section">
        <div className="sidebar__heading">Navigation</div>
        <nav aria-label="Primary">
          <ul className="sidebar__list">
            {links.map((link) => (
              <li key={link.label}>
                <button className="sidebar__link" type="button">
                  <span className="sidebar__link-label">{link.label}</span>
                  {!collapsed && (
                    <span className="sidebar__link-caption">{link.description}</span>
                  )}
                </button>
              </li>
            ))}
          </ul>
        </nav>
      </div>
      <div className="sidebar__section">
        <div className="sidebar__heading">Shortcuts</div>
        <div className="sidebar__pills">
          {"Planning CRM Docs".split(" ").map((pill) => (
            <button key={pill} className="pill" type="button">
              {pill}
            </button>
          ))}
        </div>
      </div>
    </aside>
  );
};

export default Sidebar;
