import Layout from "./components/Layout";

const App = () => {
  return (
    <Layout>
      <section className="page__header">
        <div>
          <p className="eyebrow">Workspace overview</p>
          <h1>Build knowledge together</h1>
          <p className="lede">
            A responsive canvas for documenting decisions, sharing ideas, and collaborating without friction. Optimized
            for thumb-friendly actions and readable text sizes on any device.
          </p>
          <div className="actions">
            <button className="primary-button" type="button">
              Create page
            </button>
            <button className="ghost-button" type="button">
              Invite teammates
            </button>
          </div>
        </div>
        <div className="stats">
          {[{ label: "Spaces", value: "12" }, { label: "Pages", value: "248" }, { label: "Comments", value: "1.4k" }].map(
            (stat) => (
              <div key={stat.label} className="stat-card">
                <div className="stat-card__value">{stat.value}</div>
                <div className="stat-card__label">{stat.label}</div>
              </div>
            ),
          )}
        </div>
      </section>

      <section className="grid">
        {[
          {
            title: "Recently viewed",
            description: "Jump back into the pages you visited this week.",
            items: ["Product strategy", "Quarterly OKRs", "Incident RCAs"],
          },
          {
            title: "Pinned spaces",
            description: "Favorites for quick access on mobile.",
            items: ["CRM playbooks", "Engineering", "Leadership updates"],
          },
          {
            title: "Drafts",
            description: "Work in progress across devices.",
            items: ["Mobile polish", "New onboarding", "API cookbook"],
          },
        ].map((panel) => (
          <article key={panel.title} className="card">
            <header>
              <h2>{panel.title}</h2>
              <p>{panel.description}</p>
            </header>
            <ul>
              {panel.items.map((item) => (
                <li key={item}>
                  <button className="pill pill--ghost" type="button">
                    {item}
                  </button>
                </li>
              ))}
            </ul>
          </article>
        ))}
      </section>

      <section className="panel">
        <div>
          <h2>Offline-ready notes</h2>
          <p>
            Capture ideas even when you&apos;re on the go. The editor keeps generous padding and typography so your thumbs
            have room to work.
          </p>
          <div className="actions">
            <button className="ghost-button" type="button">
              Preview mobile
            </button>
            <button className="primary-button" type="button">
              Continue writing
            </button>
          </div>
        </div>
        <div className="canvas">
          <div className="canvas__toolbar">
            <span className="pill">H1</span>
            <span className="pill">Quote</span>
            <span className="pill">Checklist</span>
            <span className="pill pill--ghost">Media</span>
          </div>
          <div className="canvas__body">
            <p className="eyebrow">Mobile-friendly canvas</p>
            <p>
              Editors and cards breathe a bit more on smaller screens, with line lengths that stay readable and tap targets
              that respect thumb reach.
            </p>
            <div className="canvas__grid">
              {["Swipe left to close", "Tap to pin", "Hold to reorder"].map((tip) => (
                <div key={tip} className="canvas__tile">
                  <span className="icon">👆</span>
                  <p>{tip}</p>
                </div>
              ))}
            </div>
          </div>
        </div>
      </section>
    </Layout>
  );
};

export default App;
