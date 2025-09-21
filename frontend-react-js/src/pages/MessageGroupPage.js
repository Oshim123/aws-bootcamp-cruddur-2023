import './MessageGroupPage.css';
import React from "react";
import { useParams } from 'react-router-dom';

import DesktopNavigation from '../components/DesktopNavigation';
import MessageGroupFeed from '../components/MessageGroupFeed';
import MessagesFeed from '../components/MessageFeed';
import MessagesForm from '../components/MessageForm';

// ✅ Amplify v6 imports
import { getCurrentUser, fetchAuthSession } from 'aws-amplify/auth';

export default function MessageGroupPage() {
  const [messageGroups, setMessageGroups] = React.useState([]);
  const [messages, setMessages] = React.useState([]);
  const [popped, setPopped] = React.useState(false);
  const [user, setUser] = React.useState(null);
  const dataFetchedRef = React.useRef(false);
  const params = useParams();

  const loadMessageGroupsData = async () => {
    try {
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/message_groups`;

      let headers = { 'Content-Type': 'application/json' };
      try {
        const session = await fetchAuthSession();
        if (session?.tokens?.idToken) {
          headers['Authorization'] = `Bearer ${session.tokens.idToken.toString()}`;
        }
      } catch (authErr) {
        console.log("No auth session", authErr);
      }

      const res = await fetch(backend_url, {
        method: "GET",
        headers: headers
      });

      let resJson = await res.json();
      if (res.status === 200) {
        setMessageGroups(resJson);
      } else {
        console.log("Backend error:", res.status, resJson);
      }
    } catch (err) {
      console.log("Fetch error:", err);
    }
  };

  const loadMessageGroupData = async () => {
    try {
      const handle = `@${params.handle}`;
      const backend_url = `${process.env.REACT_APP_BACKEND_URL}/api/messages/${handle}`;

      let headers = { 'Content-Type': 'application/json' };
      try {
        const session = await fetchAuthSession();
        if (session?.tokens?.idToken) {
          headers['Authorization'] = `Bearer ${session.tokens.idToken.toString()}`;
        }
      } catch (authErr) {
        console.log("No auth session", authErr);
      }

      const res = await fetch(backend_url, {
        method: "GET",
        headers: headers
      });

      let resJson = await res.json();
      if (res.status === 200) {
        setMessages(resJson);
      } else {
        console.log("Backend error:", res.status, resJson);
      }
    } catch (err) {
      console.log("Fetch error:", err);
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

    loadMessageGroupsData();
    loadMessageGroupData();
    checkAuth();
  }, []);

  return (
    <article>
      <DesktopNavigation user={user} active={'home'} setPopped={setPopped} />
      <section className='message_groups'>
        <MessageGroupFeed message_groups={messageGroups} />
      </section>
      <div className='content messages'>
        <MessagesFeed messages={messages} />
        <MessagesForm setMessages={setMessages} />
      </div>
    </article>
  );
}
