// HomeFeedPage.js - Improved version with proper v6 auth
import './HomeFeedPage.css';
import React from "react";

// ✅ Amplify v6 imports
import { getCurrentUser, fetchAuthSession } from 'aws-amplify/auth';

import DesktopNavigation from '../components/DesktopNavigation';
import DesktopSidebar from '../components/DesktopSidebar';
import ActivityFeed from '../components/ActivityFeed';
import ActivityForm from '../components/ActivityForm';
import ReplyForm from '../components/ReplyForm';

export default function HomeFeedPage() {
  const [activities, setActivities] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [poppedReply, setPoppedReply] = React.useState(false);
  const [replyActivity, setReplyActivity] = React.useState({});
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);

  const loadData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/activities/home`;
      
      let headers = {
        'Content-Type': 'application/json'
      };

      // Try to get v6 auth session
      try {
        const session = await fetchAuthSession();
        if (session?.tokens?.accessToken) {
          headers['Authorization'] = `Bearer ${session.tokens.accessToken.toString()}`;
        }
      } catch (authErr) {
        // If no auth session, try fallback to localStorage (for compatibility)
        const token = localStorage.getItem("access_token");
        if (token) {
          headers['Authorization'] = `Bearer ${token}`;
        }
      }

      const res = await fetch(backend_url, {
        headers: headers,
        method: "GET"
      });

      let resJson = await res.json();
      if (res.status === 200) {
        setActivities(resJson);
      } else {
        console.log(res);
      }
    } catch (err) {
      console.log(err);
    }
  };

  const checkAuth = async () => {
    try {
      const cognito_user = await getCurrentUser();
      console.log('user', cognito_user);
      setUser({
        display_name: cognito_user.signInDetails?.loginId || cognito_user.username,
        handle: cognito_user.username
      });
    } catch (err) {
      console.log("No authenticated user", err);
    }
  };

  React.useEffect(() => {
    if (dataFetchedRef.current) return;
    dataFetchedRef.current = true;

    loadData();
    checkAuth();
  }, []);

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <div className='content'>
        <ActivityForm
          popped={popped}
          setPopped={setPopped}
          setActivities={setActivities}
        />
        <ReplyForm
          activity={replyActivity}
          popped={poppedReply}
          setPopped={setPoppedReply}
          setActivities={setActivities}
          activities={activities}
        />
        <ActivityFeed
          title="Home"
          setReplyActivity={setReplyActivity}
          setPopped={setPoppedReply}
          activities={activities}
        />
      </div>
      <DesktopSidebar user={user} />
    </article>
  );
}