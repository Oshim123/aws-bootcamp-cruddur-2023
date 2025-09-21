import './App.css';

import HomeFeedPage from './pages/HomeFeedPage';
import UserFeedPage from './pages/UserFeedPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import RecoverPage from './pages/RecoverPage';
import MessageGroupsPage from './pages/MessageGroupsPage';
import MessageGroupPage from './pages/MessageGroupPage';
import ConfirmationPage from './pages/ConfirmationPage';
import NotificationsFeedPage from './pages/NotificationsFeedPage';

import React from 'react';
import { createBrowserRouter, RouterProvider } from "react-router-dom";

// ✅ Amplify v6 imports
import { Amplify } from 'aws-amplify';

// ✅ Amplify v6 configuration (your EU West 2 Cognito settings)
Amplify.configure({
  Auth: {
    Cognito: {
      region: 'eu-west-2',
      userPoolId: 'eu-west-2_HKcHnrgiB',
      userPoolClientId: 'cte794vg6jirnr3eqtt2v500i',
      loginWith: {
        email: true // allow sign-in with email
      }
    }
  }
});

// ✅ React Router setup
const router = createBrowserRouter([
  { path: "/", element: <HomeFeedPage /> },
  { path: "/@:handle", element: <UserFeedPage /> },
  { path: "/messages", element: <MessageGroupsPage /> },
  { path: "/messages/@:handle", element: <MessageGroupPage /> },
  { path: "/signup", element: <SignupPage /> },
  { path: "/signin", element: <SigninPage /> },
  { path: "/confirm", element: <ConfirmationPage /> },
  { path: "/forgot", element: <RecoverPage /> },
  { path: "/notifications", element: <NotificationsFeedPage /> } // 👈 added
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
