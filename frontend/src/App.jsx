import { Route, Routes } from "react-router-dom";

import Footer from "./components/Footer";
import NavBar from "./components/NavBar";
import ProtectedRoute from "./components/ProtectedRoute";
import AboutPage from "./pages/AboutPage";
import ContactPage from "./pages/ContactPage";
import CreatorPage from "./pages/CreatorPage";
import FaqPage from "./pages/FaqPage";
import HelpCenterPage from "./pages/HelpCenterPage";
import HomePage from "./pages/HomePage";
import LoginPage from "./pages/LoginPage";
import PrivacyPage from "./pages/PrivacyPage";
import SignupPage from "./pages/SignupPage";
import StoryReaderPage from "./pages/StoryReaderPage";
import TermsPage from "./pages/TermsPage";

const App = () => {
  return (
    <div className="flex min-h-screen flex-col">
      <NavBar />
      <main className="mx-auto w-full max-w-6xl flex-1 px-4 py-8">
        <Routes>
          <Route path="/" element={<HomePage />} />
          <Route path="/stories/:storyId" element={<StoryReaderPage />} />
          <Route path="/login" element={<LoginPage />} />
          <Route path="/signup" element={<SignupPage />} />
          <Route path="/about" element={<AboutPage />} />
          <Route path="/contact" element={<ContactPage />} />
          <Route path="/faq" element={<FaqPage />} />
          <Route path="/help" element={<HelpCenterPage />} />
          <Route path="/privacy" element={<PrivacyPage />} />
          <Route path="/terms" element={<TermsPage />} />
          <Route
            path="/creator"
            element={
              <ProtectedRoute>
                <CreatorPage />
              </ProtectedRoute>
            }
          />
        </Routes>
      </main>
      <Footer />
    </div>
  );
};

export default App;
