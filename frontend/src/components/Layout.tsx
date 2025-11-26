import { useEffect, useMemo, useRef, useState } from "react";
import type { PointerEvent, ReactNode } from "react";
import BottomNav from "./BottomNav";
import Drawer from "./Drawer";
import Sidebar from "./Sidebar";
import TopBar from "./TopBar";

type LayoutProps = {
  children: ReactNode;
};

const useMediaQuery = (query: string) => {
  const getMatch = () => (typeof window !== "undefined" ? matchMedia(query).matches : false);
  const [matches, setMatches] = useState(getMatch);

  useEffect(() => {
    if (typeof window === "undefined") return undefined;

    const media = matchMedia(query);
    const listener = () => setMatches(media.matches);
    media.addEventListener("change", listener);
    return () => media.removeEventListener("change", listener);
  }, [query]);

  return matches;
};

const Layout = ({ children }: LayoutProps) => {
  const isTablet = useMediaQuery("(max-width: 1024px)");
  const isMobile = useMediaQuery("(max-width: 768px)");
  const [drawerOpen, setDrawerOpen] = useState(false);
  const gestureStartX = useRef<number | null>(null);

  useEffect(() => {
    if (!isTablet) {
      setDrawerOpen(false);
    }
  }, [isTablet]);

  const enableGestures = useMemo(() => isTablet, [isTablet]);

  const handlePointerDown = (event: PointerEvent<HTMLElement>) => {
    if (!enableGestures) return;
    gestureStartX.current = event.clientX;
  };

  const handlePointerUp = (event: PointerEvent<HTMLElement>) => {
    if (!enableGestures || gestureStartX.current === null) return;
    const deltaX = event.clientX - gestureStartX.current;

    if (!drawerOpen && gestureStartX.current < 32 && deltaX > 50) {
      setDrawerOpen(true);
    }

    if (drawerOpen && deltaX < -50) {
      setDrawerOpen(false);
    }

    gestureStartX.current = null;
  };

  return (
    <div className="app-shell" onPointerDown={handlePointerDown} onPointerUp={handlePointerUp}>
      <TopBar onMenuToggle={() => setDrawerOpen((open) => !open)} isDrawerOpen={drawerOpen} />
      <div className="content-shell">
        {isTablet ? (
          <Drawer open={drawerOpen} onClose={() => setDrawerOpen(false)}>
            <Sidebar collapsed={isMobile} />
          </Drawer>
        ) : (
          <Sidebar />
        )}
        <main className="page" aria-label="Workspace content">
          {children}
        </main>
      </div>
      {isMobile && <BottomNav onMenuToggle={() => setDrawerOpen((open) => !open)} />}
    </div>
  );
};

export default Layout;
