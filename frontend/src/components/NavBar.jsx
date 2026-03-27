import { useEffect, useRef, useState } from "react";
import { Link, NavLink, useNavigate } from "react-router-dom";

import { useAuth } from "../context/AuthContext";

const navLinks = [
  { label: "Stories", to: "/" },
  { label: "About", to: "/about" },
  { label: "FAQ", to: "/faq" },
  { label: "Contact", to: "/contact" }
];

const getLinkClassName = ({ isActive }) =>
  `transition hover:text-ember ${isActive ? "text-ink font-semibold" : ""}`;

const NavBar = () => {
  const { user, isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [isProfileMenuOpen, setIsProfileMenuOpen] = useState(false);
  const profileMenuRef = useRef(null);

  useEffect(() => {
    const onDocumentMouseDown = (event) => {
      if (profileMenuRef.current && !profileMenuRef.current.contains(event.target)) {
        setIsProfileMenuOpen(false);
      }
    };

    const onDocumentKeyDown = (event) => {
      if (event.key === "Escape") {
        setIsProfileMenuOpen(false);
      }
    };

    document.addEventListener("mousedown", onDocumentMouseDown);
    document.addEventListener("keydown", onDocumentKeyDown);
    return () => {
      document.removeEventListener("mousedown", onDocumentMouseDown);
      document.removeEventListener("keydown", onDocumentKeyDown);
    };
  }, []);

  const onLogout = async () => {
    setIsProfileMenuOpen(false);
    await logout();
    navigate("/");
  };

  return (
    <header className="sticky top-0 z-20 border-b border-white/20 bg-white/65 backdrop-blur-md">
      <nav className="mx-auto flex w-full max-w-6xl flex-col gap-3 px-4 py-3 md:flex-row md:items-center md:justify-between">
        <div className="flex items-center justify-between">
          <Link to="/" className="text-lg font-bold tracking-tight text-ink">
            TaleForge
          </Link>
        </div>

        <div className="flex flex-wrap items-center gap-3 text-sm font-medium text-dusk">
          {navLinks.map((link) => (
            <NavLink key={link.to} to={link.to} className={getLinkClassName}>
              {link.label}
            </NavLink>
          ))}

          {isAuthenticated && (
            <NavLink className={getLinkClassName} to="/creator">
              Create
            </NavLink>
          )}

          {isAuthenticated ? (
            <div ref={profileMenuRef} className="relative ml-auto">
              <button
                type="button"
                aria-label="Open profile menu"
                aria-expanded={isProfileMenuOpen}
                aria-haspopup="menu"
                onClick={() => setIsProfileMenuOpen((prev) => !prev)}
                className="flex h-10 w-10 items-center justify-center rounded-full border border-slate-300 bg-white text-dusk transition hover:border-slate-500 hover:text-ink"
              >
                <svg viewBox="0 0 24 24" className="h-5 w-5" fill="none" stroke="currentColor" strokeWidth="1.8">
                  <circle cx="12" cy="8" r="4" />
                  <path d="M4 20a8 8 0 0 1 16 0" />
                </svg>
              </button>

              {isProfileMenuOpen && (
                <div className="absolute right-0 top-12 z-30 w-48 rounded-xl border border-slate-200 bg-white p-2 shadow-soft">
                  <p className="border-b border-slate-100 px-3 py-2 text-sm font-semibold text-ink">
                    {user?.username}
                  </p>
                  <button
                    onClick={onLogout}
                    className="mt-1 w-full rounded-lg px-3 py-2 text-left text-sm font-medium text-dusk transition hover:bg-slate-100 hover:text-ink"
                  >
                    Logout
                  </button>
                </div>
              )}
            </div>
          ) : (
            <div className="ml-auto flex items-center gap-2 whitespace-nowrap">
              <Link className="hover:text-ember" to="/login">
                Login
              </Link>
              <Link className="rounded-lg bg-ink px-3 py-1.5 text-white transition hover:bg-dusk" to="/signup">
                Sign up
              </Link>
            </div>
          )}
        </div>
      </nav>
    </header>
  );
};

export default NavBar;
