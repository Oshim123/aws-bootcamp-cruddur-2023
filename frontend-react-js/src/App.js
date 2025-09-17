import './App.css';

import HomeFeedPage from './pages/HomeFeedPage';
import UserFeedPage from './pages/UserFeedPage';
import SignupPage from './pages/SignupPage';
import SigninPage from './pages/SigninPage';
import RecoverPage from './pages/RecoverPage';
import MessageGroupsPage from './pages/MessageGroupsPage';
import MessageGroupPage from './pages/MessageGroupPage';
import ConfirmationPage from './pages/ConfirmationPage';

import React from 'react';
import { createBrowserRouter, RouterProvider } from "react-router-dom";

import { Amplify } from 'aws-amplify';

// ✅ Amplify configuration (v6 format only)
// Remove old keys like AWS_PROJECT_REGION / aws_cognito_region
// Keep only the Auth block
Amplify.configure({
  Auth: {
    region: "eu-west-2",                        // your region
    userPoolId: "eu-west-2_HKcHnrgiB",          // your User Pool ID
    userPoolWebClientId: "cte794vg6jirnr3eqtt2v500i" // your App Client ID
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
  { path: "/forgot", element: <RecoverPage /> }
]);

function App() {
  return <RouterProvider router={router} />;
}

export default App;
