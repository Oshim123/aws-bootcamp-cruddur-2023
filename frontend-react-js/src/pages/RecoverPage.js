import './RecoverPage.css';
import React from "react";
import { ReactComponent as Logo } from '../components/svg/logo.svg';
import { Link } from "react-router-dom";

// ✅ Amplify v6 Auth imports
import { resetPassword, confirmResetPassword } from "aws-amplify/auth";

export default function RecoverPage() {
  const [username, setUsername] = React.useState('');
  const [password, setPassword] = React.useState('');
  const [passwordAgain, setPasswordAgain] = React.useState('');
  const [code, setCode] = React.useState('');
  const [errors, setErrors] = React.useState('');
  const [formState, setFormState] = React.useState('send_code');

  const onsubmit_send_code = async (event) => {
    event.preventDefault();
    setErrors('');
    try {
      await resetPassword({ username });
      setFormState('confirm_code');
    } catch (err) {
      console.error("Reset error:", err);
      setErrors(err.message);
    }
    return false;
  };

  const onsubmit_confirm_code = async (event) => {
    event.preventDefault();
    setErrors('');
    if (password !== passwordAgain) {
      setErrors('Passwords do not match');
      return false;
    }
    try {
      await confirmResetPassword({ username, confirmationCode: code, newPassword: password });
      setFormState('success');
    } catch (err) {
      console.error("Confirm reset error:", err);
      setErrors(err.message);
    }
    return false;
  };

  let el_errors;
  if (errors) {
    el_errors = <div className='errors'>{errors}</div>;
  }

  const send_code = () => (
    <form className='recover_form' onSubmit={onsubmit_send_code}>
      <h2>Recover your Password</h2>
      <div className='fields'>
        <div className='field text_field username'>
          <label>Email</label>
          <input
            type="text"
            value={username}
            onChange={(e) => setUsername(e.target.value)} 
          />
        </div>
      </div>
      {el_errors}
      <div className='submit'>
        <button type='submit'>Send Recovery Code</button>
      </div>
    </form>
  );

  const confirm_code = () => (
    <form className='recover_form' onSubmit={onsubmit_confirm_code}>
      <h2>Recover your Password</h2>
      <div className='fields'>
        <div className='field text_field code'>
          <label>Reset Password Code</label>
          <input
            type="text"
            value={code}
            onChange={(e) => setCode(e.target.value)} 
          />
        </div>
        <div className='field text_field password'>
          <label>New Password</label>
          <input
            type="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)} 
          />
        </div>
        <div className='field text_field password_again'>
          <label>New Password Again</label>
          <input
            type="password"
            value={passwordAgain}
            onChange={(e) => setPasswordAgain(e.target.value)} 
          />
        </div>
      </div>
      {el_errors}
      <div className='submit'>
        <button type='submit'>Reset Password</button>
      </div>
    </form>
  );

  const success = () => (
    <form>
      <p>Your password has been successfully reset!</p>
      <Link to="/signin" className="proceed">Proceed to Signin</Link>
    </form>
  );

  let form;
  if (formState === 'send_code') {
    form = send_code();
  } else if (formState === 'confirm_code') {
    form = confirm_code();
  } else if (formState === 'success') {
    form = success();
  }

  return (
    <article className="recover-article">
      <div className='recover-info'>
        <Logo className='logo' />
      </div>
      <div className='recover-wrapper'>
        {form}
      </div>
    </article>
  );
}
