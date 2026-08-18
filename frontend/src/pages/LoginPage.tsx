import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import type { User } from '../types';

export default function LoginPage() {
  const navigate = useNavigate();
  const [isLogin, setIsLogin] = useState(true);
  const [phone, setPhone] = useState('');
  const [password, setPassword] = useState('');
  const [name, setName] = useState('');
  const [error, setError] = useState('');
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const tokens = localStorage.getItem('tokens');
    if (tokens) navigate('/feed', { replace: true });
  }, [navigate]);

  const handleSubmit = async (e: React.FormEvent) => {
    e.preventDefault();
    setError('');
    setLoading(true);

    try {
      if (isLogin) {
        const res = await api.post('/auth/token/', { phone, password });
        localStorage.setItem('tokens', JSON.stringify(res.data));
        const userRes = await api.get('/users/me/');
        localStorage.setItem('user', JSON.stringify(userRes.data));
        const user: User = userRes.data;
        if (!user.profile_complete) {
          navigate('/setup', { replace: true });
        } else {
          navigate('/feed', { replace: true });
        }
      } else {
        const res = await api.post('/auth/register/', { phone, password, name });
        localStorage.setItem('tokens', JSON.stringify(res.data.tokens));
        localStorage.setItem('user', JSON.stringify(res.data.user));
        navigate('/setup', { replace: true });
      }
    } catch (err: any) {
      const msg = err.response?.data?.detail ||
        err.response?.data?.phone?.[0] ||
        err.response?.data?.password?.[0] ||
        err.response?.data?.error ||
        'Ошибка';
      setError(msg);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div className="auth-page">
      <div className="auth-logo">
        <h1>FlatMate</h1>
        <p>Найди соседа и жильё мечты</p>
      </div>

      <form className="auth-form" onSubmit={handleSubmit}>
        {error && <div className="auth-error">{error}</div>}

        <div className="input-group">
          <label>Телефон</label>
          <input
            type="tel"
            placeholder="+7 900 123 45 67"
            value={phone}
            onChange={(e) => setPhone(e.target.value)}
            required
          />
        </div>

        {!isLogin && (
          <div className="input-group">
            <label>Имя</label>
            <input
              type="text"
              placeholder="Как тебя зовут?"
              value={name}
              onChange={(e) => setName(e.target.value)}
            />
          </div>
        )}

        <div className="input-group">
          <label>Пароль</label>
          <input
            type="password"
            placeholder="Минимум 6 символов"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            minLength={6}
            required
          />
        </div>

        <button className="btn btn-primary" type="submit" disabled={loading}>
          {loading ? <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }} /> :
            isLogin ? 'Войти' : 'Создать аккаунт'}
        </button>
      </form>

      <div className="auth-switch">
        {isLogin ? (
          <>Нет аккаунта? <a href="#" onClick={(e) => { e.preventDefault(); setIsLogin(false); setError(''); }}>Зарегистрироваться</a></>
        ) : (
          <>Уже есть аккаунт? <a href="#" onClick={(e) => { e.preventDefault(); setIsLogin(true); setError(''); }}>Войти</a></>
        )}
      </div>
    </div>
  );
}
