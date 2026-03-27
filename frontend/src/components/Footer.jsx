import { Link } from "react-router-dom";

const footerLinks = [
  { label: "About Us", to: "/about" },
  { label: "Contact Us", to: "/contact" },
  { label: "FAQ", to: "/faq" },
  { label: "Help Center", to: "/help" },
  { label: "Privacy Policy", to: "/privacy" },
  { label: "Terms of Service", to: "/terms" }
];

const Footer = () => {
  return (
    <footer className="border-t border-white/30 bg-white/60 backdrop-blur-md">
      <div className="mx-auto w-full max-w-6xl px-4 py-8">
        <div className="grid gap-6 md:grid-cols-2">
          <div>
            <h2 className="text-lg font-bold text-ink">TaleForge</h2>
            <p className="mt-2 max-w-md text-sm text-slate-600">
              Craft and explore interactive stories where every decision changes the path.
            </p>
          </div>
          <div className="grid grid-cols-2 gap-3 text-sm text-slate-700 sm:grid-cols-3">
            {footerLinks.map((link) => (
              <Link key={link.to} to={link.to} className="transition hover:text-ember">
                {link.label}
              </Link>
            ))}
          </div>
        </div>

        <div className="mt-7 border-t border-slate-200 pt-4 text-xs text-slate-500">
          © {new Date().getFullYear()} TaleForge. All rights reserved.
        </div>
      </div>
    </footer>
  );
};

export default Footer;
