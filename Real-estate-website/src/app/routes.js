import MainLayout from "../components/MainLayout";
import Home from "../components/home/Home";
import Pages from "../components/pages/Pages";
import Agent from "../components/Agent/Agent";
import Services from "../components/services/Services";
import Blog from "../components/blog/Blog";
import Pricing from "../components/pricing/Pricing";
import Contact from "../components/contact/Contact";
import SignUp from "../components/Auth/SignUp";
import SignIn from "../components/Auth/SignIn";

const routes = [
   {
      path: '/',
      element: <Pages />,
      children: [
         { path: '/', element: <Home /> },
         { path: '/agent', element: <Agent /> },
         { path: '/services', element: <Services /> },
         { path: '/blog', element: <Blog />},
         { path: '/pricing', element: <Pricing />},
         { path: '/contact', element: <Contact />}
      ],
   },
   {
      path: '/auth',
      element: <MainLayout />,
      children: [
         { path: 'login', element: <SignIn /> },
         { path: 'register', element: <SignUp /> },
      ],
   },
];

export default routes;
