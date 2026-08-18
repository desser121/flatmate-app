import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';

export default function SetupPage() {
  const navigate = useNavigate();
  const [step, setStep] = useState(0);
  const [name, setName] = useState('');
  const [gender, setGender] = useState('');
  const [city, setCity] = useState('');
  const [roles, setRoles] = useState({ seeker: false, roommate: false, landlord: false });
  const [loading, setLoading] = useState(false);

  useEffect(() => {
    const saved = localStorage.getItem('user');
    if (saved) {
      const u = JSON.parse(saved);
      setName(u.name || '');
      setGender(u.gender || '');
      setCity(u.city || '');
      setRoles({
        seeker: u.role_seeker,
        roommate: u.role_roommate,
        landlord: u.role_landlord,
      });
    }
  }, []);

  const toggleRole = (key: 'seeker' | 'roommate' | 'landlord') => {
    setRoles(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const cities = ['Москва', 'Санкт-Петербург', 'Казань', 'Новосибирск', 'Екатеринбург', 'Краснодар', 'Сочи', 'Другой'];

  const handleFinish = async () => {
    setLoading(true);
    try {
      await api.put('/users/me/', {
        name,
        gender,
        city,
        role_seeker: roles.seeker,
        role_roommate: roles.roommate,
        role_landlord: roles.landlord,
      });
      const userRes = await api.get('/users/me/');
      localStorage.setItem('user', JSON.stringify(userRes.data));
      navigate('/feed', { replace: true });
    } catch {
    } finally {
      setLoading(false);
    }
  };

  const steps = [
    // Step 0: Name
    <div className="setup-form" key="name">
      <div className="input-group">
        <label>Как тебя зовут?</label>
        <input
          type="text"
          placeholder="Введи имя"
          value={name}
          onChange={(e) => setName(e.target.value)}
        />
      </div>
    </div>,

    // Step 1: Gender
    <div className="setup-form" key="gender">
      <div className="role-options">
        {[
          { key: 'male', icon: '👨', label: 'Мужской' },
          { key: 'female', icon: '👩', label: 'Женский' },
          { key: 'other', icon: '⚧', label: 'Другой' },
        ].map(g => (
          <div
            key={g.key}
            className={`role-option ${gender === g.key ? 'selected' : ''}`}
            onClick={() => setGender(g.key)}
          >
            <div className="role-option-icon">{g.icon}</div>
            <div className="role-option-text">
              <h4>{g.label}</h4>
            </div>
          </div>
        ))}
      </div>
    </div>,

    // Step 2: City
    <div className="setup-form" key="city">
      <div className="role-options">
        {cities.map(c => (
          <div
            key={c}
            className={`role-option ${city === c ? 'selected' : ''}`}
            onClick={() => setCity(c)}
          >
            <div className="role-option-icon">📍</div>
            <div className="role-option-text">
              <h4>{c}</h4>
            </div>
          </div>
        ))}
      </div>
    </div>,

    // Step 3: Roles
    <div className="setup-form" key="roles">
      <div className="role-options">
        <div className={`role-option ${roles.seeker ? 'selected' : ''}`} onClick={() => toggleRole('seeker')}>
          <div className="role-option-icon">🏠</div>
          <div className="role-option-text">
            <h4>Ищу жильё</h4>
            <p>Ищу квартиру или комнату для аренды</p>
          </div>
        </div>
        <div className={`role-option ${roles.roommate ? 'selected' : ''}`} onClick={() => toggleRole('roommate')}>
          <div className="role-option-icon">👥</div>
          <div className="role-option-text">
            <h4>Ищу соседа</h4>
            <p>Уже снимаю ищу человека для совместной аренды</p>
          </div>
        </div>
        <div className={`role-option ${roles.landlord ? 'selected' : ''}`} onClick={() => toggleRole('landlord')}>
          <div className="role-option-icon">🔑</div>
          <div className="role-option-text">
            <h4>Сдаю жильё</h4>
            <p>У меня есть жильё, которое я хочу сдать</p>
          </div>
        </div>
      </div>
    </div>,
  ];

  const canNext = () => {
    if (step === 0) return name.length > 0;
    if (step === 1) return gender !== '';
    if (step === 2) return city !== '';
    if (step === 3) return roles.seeker || roles.roommate || roles.landlord;
    return false;
  };

  return (
    <div className="setup-page">
      <div className="setup-header">
        <h2>Настройка профиля</h2>
        <p>Расскажи о себе, чтобы найти идеального соседа</p>
      </div>

      <div className="setup-progress">
        {[0, 1, 2, 3].map(i => (
          <div key={i} className={`dot ${i <= step ? 'active' : ''}`} />
        ))}
      </div>

      {steps[step]}

      <div className="setup-footer">
        <div style={{ display: 'flex', gap: 12 }}>
          {step > 0 && (
            <button className="btn btn-ghost" onClick={() => setStep(s => s - 1)}>
              Назад
            </button>
          )}
          {step < 3 ? (
            <button className="btn btn-primary" onClick={() => setStep(s => s + 1)} disabled={!canNext()}>
              Далее
            </button>
          ) : (
            <button className="btn btn-primary" onClick={handleFinish} disabled={loading || !canNext()}>
              {loading ? <div className="spinner" style={{ width: 20, height: 20, borderWidth: 2 }} /> : 'Начать'}
            </button>
          )}
        </div>
      </div>
    </div>
  );
}
