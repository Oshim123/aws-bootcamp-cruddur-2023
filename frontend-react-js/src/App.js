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

// ✅ Amplify configuration
Amplify.configure({
  "AWS_PROJECT_REGION": process.env.REACT_APP_AWS_PROJECT_REGION,      // e.g. eu-west-2
  "aws_cognito_region": process.env.REACT_APP_AWS_COGNITO_REGION,      // usually same as project region
  "aws_user_pools_id": process.env.REACT_APP_AWS_USER_POOLS_ID,        // e.g. eu-west-2_AbCdEf123
  "aws_user_pools_web_client_id": process.env.REACT_APP_CLIENT_ID,     // your Cognito App Client ID
  Auth: {
    region: process.env.REACT_APP_AWS_PROJECT_REGION,                  
    userPoolId: process.env.REACT_APP_AWS_USER_POOLS_ID,               
    userPoolWebClientId: process.env.REACT_APP_CLIENT_ID               
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
