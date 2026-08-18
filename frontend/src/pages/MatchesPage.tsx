import { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import api from '../services/api';
import type { Match } from '../types';

export default function MatchesPage() {
  const navigate = useNavigate();
  const [matches, setMatches] = useState<Match[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    const fetchMatches = async () => {
      try {
        const res = await api.get('/matches/');
        setMatches(res.data.results || res.data || []);
      } catch {
      } finally {
        setLoading(false);
      }
    };
    fetchMatches();
  }, []);

  const handleOpenChat = (matchId: string) => {
    navigate(`/chat/${matchId}`);
  };

  if (loading) {
    return (
      <div className="main-layout">
        <div className="header">
          <h2>Матчи</h2>
        </div>
        <div className="page-content">
          <div className="loading"><div className="spinner" /></div>
        </div>
      </div>
    );
  }

  return (
    <div className="main-layout">
      <div className="header">
        <h2>Матчи</h2>
      </div>
      <div className="page-content">
        {matches.length === 0 ? (
          <div className="empty-state" style={{ paddingTop: 80 }}>
            <h3>Пока нет матчей</h3>
            <p>Ставь лайки на анкеты, чтобы найти своего человека</p>
          </div>
        ) : (
          <div className="matches-grid">
            {matches.map((match) => {
              const other = match.other_user;
              const primaryPhoto = other.photos?.find(p => p.is_primary) || other.photos?.[0];

              return (
                <div key={match.id} className="match-item" onClick={() => handleOpenChat(match.id)}>
                  {primaryPhoto ? (
                    <img className="match-avatar" src={primaryPhoto.image} alt={other.name} />
                  ) : (
                    <div className="match-avatar-placeholder">
                      {other.name?.charAt(0) || '?'}
                    </div>
                  )}
                  <div className="match-info">
                    <div className="match-name">{other.name}{other.age ? `, ${other.age}` : ''}</div>
                    <div className="match-last-msg">Начни общение!</div>
                  </div>
                  <div className="match-meta">
                    <span className="match-time">сейчас</span>
                  </div>
                </div>
              );
            })}
          </div>
        )}
      </div>
    </div>
  );
}
