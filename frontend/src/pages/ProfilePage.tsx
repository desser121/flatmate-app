import { useEffect, useState } from 'react';
import { useNavigate } from 'react-router-dom';
import type { User } from '../types';

export default function ProfilePage() {
  const navigate = useNavigate();
  const [user, setUser] = useState<User | null>(null);

  useEffect(() => {
    const saved = localStorage.getItem('user');
    if (saved) {
      setUser(JSON.parse(saved));
    }
  }, []);

  const handleLogout = () => {
    localStorage.removeItem('tokens');
    localStorage.removeItem('user');
    navigate('/login', { replace: true });
  };

  if (!user) return <div className="loading"><div className="spinner" /></div>;

  return (
    <div className="main-layout">
      <div className="header">
        <h2>Профиль</h2>
      </div>
      <div className="page-content">
        <div className="profile-page">
          <div className="profile-avatar-section">
            {user.photos?.[0] ? (
              <img className="profile-avatar" src={user.photos[0].image} alt={user.name} />
            ) : (
              <div className="profile-avatar-placeholder">{user.name?.charAt(0) || '?'}</div>
            )}
            <div className="profile-name">{user.name}</div>
            <div className="profile-city">📍 {user.city || 'Не указан'}</div>
          </div>

          <div className="profile-section">
            <h3>Роли</h3>
            <div className="profile-roles">
              <span className={`role-badge ${user.role_seeker ? 'active' : ''}`}>🏠 Ищу жильё</span>
              <span className={`role-badge ${user.role_roommate ? 'active' : ''}`}>👥 Ищу соседа</span>
              <span className={`role-badge ${user.role_landlord ? 'active' : ''}`}>🔑 Сдаю жильё</span>
            </div>
          </div>

          <div className="profile-section">
            <h3>Данные</h3>
            <div className="profile-details">
              <div className="detail-row">
                <span className="detail-label">Телефон</span>
                <span className="detail-value">{user.phone}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Возраст</span>
                <span className="detail-value">{user.age || 'Не указан'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Пол</span>
                <span className="detail-value">{user.gender === 'male' ? 'Мужской' : user.gender === 'female' ? 'Женский' : user.gender || 'Не указан'}</span>
              </div>
              <div className="detail-row">
                <span className="detail-label">Город</span>
                <span className="detail-value">{user.city || 'Не указан'}</span>
              </div>
            </div>
          </div>

          {user.bio && (
            <div className="profile-section">
              <h3>О себе</h3>
              <div style={{ color: 'var(--text-secondary)', fontSize: 14, lineHeight: 1.5 }}>{user.bio}</div>
            </div>
          )}

          <div className="profile-actions">
            <button className="btn btn-ghost" onClick={handleLogout}>
              Выйти из аккаунта
            </button>
          </div>
        </div>
      </div>
    </div>
  );
}
