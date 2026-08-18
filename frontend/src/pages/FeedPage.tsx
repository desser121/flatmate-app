import { useState, useEffect, useCallback, useRef } from 'react';
import api from '../services/api';
import type { FeedItem } from '../types';

export default function FeedPage() {
  const [items, setItems] = useState<FeedItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [feedType, setFeedType] = useState<'user' | 'listing'>('user');
  const [currentIndex, setCurrentIndex] = useState(0);
  const [dragOffset, setDragOffset] = useState(0);
  const [dragging, setDragging] = useState(false);
  const startX = useRef(0);

  const fetchFeed = useCallback(async () => {
    setLoading(true);
    try {
      const res = await api.get(`/swipes/feed/?type=${feedType}&page=1`);
      setItems(res.data.items || []);
      setCurrentIndex(0);
    } catch {
    } finally {
      setLoading(false);
    }
  }, [feedType]);

  useEffect(() => { fetchFeed(); }, [fetchFeed]);

  const handleSwipe = async (action: 'like' | 'dislike') => {
    const item = items[currentIndex];
    if (!item) return;

    const nextIndex = currentIndex + 1;
    setCurrentIndex(nextIndex);
    setDragOffset(0);

    try {
      await api.post('/swipes/', {
        target_type: item.type,
        target_id: item.id,
        action,
      });
    } catch {
    }
  };

  const handleTouchStart = (e: React.TouchEvent) => {
    startX.current = e.touches[0].clientX;
    setDragging(true);
  };

  const handleTouchMove = (e: React.TouchEvent) => {
    if (!dragging) return;
    const diff = e.touches[0].clientX - startX.current;
    setDragOffset(diff);
  };

  const handleTouchEnd = () => {
    setDragging(false);
    if (dragOffset > 100) {
      handleSwipe('like');
    } else if (dragOffset < -100) {
      handleSwipe('dislike');
    } else {
      setDragOffset(0);
    }
  };

  const handleMouseDown = (e: React.MouseEvent) => {
    startX.current = e.clientX;
    setDragging(true);
  };

  const handleMouseMove = (e: React.MouseEvent) => {
    if (!dragging) return;
    const diff = e.clientX - startX.current;
    setDragOffset(diff);
  };

  const handleMouseUp = () => {
    setDragging(false);
    if (dragOffset > 100) {
      handleSwipe('like');
    } else if (dragOffset < -100) {
      handleSwipe('dislike');
    } else {
      setDragOffset(0);
    }
  };

  const visibleItems = items.slice(currentIndex, currentIndex + 2);
  const currentItem = visibleItems[0];

  return (
    <div className="feed-container">
      <div className="feed-toggle">
        <button
          className={feedType === 'user' ? 'active' : ''}
          onClick={() => setFeedType('user')}
        >
          👥 Люди
        </button>
        <button
          className={feedType === 'listing' ? 'active' : ''}
          onClick={() => setFeedType('listing')}
        >
          🏠 Жильё
        </button>
      </div>

      <div className="card-stack">
        {loading ? (
          <div className="loading"><div className="spinner" /></div>
        ) : !currentItem ? (
          <div className="empty-state">
            <h3>Пока пусто</h3>
            <p>Загрузите анкеты позже или измените фильтры поиска</p>
          </div>
        ) : (
          <>
            {visibleItems.length > 1 && (
              <div
                className="swipe-card"
                style={{
                  transform: `scale(0.95) translateY(8px)`,
                  opacity: 0.6,
                  zIndex: 0,
                }}
              >
                {visibleItems[1].type === 'user' ? (
                  <UserCard item={visibleItems[1]} />
                ) : (
                  <ListingCard item={visibleItems[1]} />
                )}
              </div>
            )}

            <div
              className="swipe-card"
              style={{
                transform: `translateX(${dragOffset}px) rotate(${dragOffset * 0.05}deg)`,
                opacity: 1 - Math.abs(dragOffset) / 400,
                zIndex: 1,
                cursor: dragging ? 'grabbing' : 'grab',
              }}
              onTouchStart={handleTouchStart}
              onTouchMove={handleTouchMove}
              onTouchEnd={handleTouchEnd}
              onMouseDown={handleMouseDown}
              onMouseMove={handleMouseMove}
              onMouseUp={handleMouseUp}
              onMouseLeave={handleMouseUp}
            >
              {currentItem.type === 'user' ? (
                <UserCard item={currentItem} />
              ) : (
                <ListingCard item={currentItem} />
              )}
            </div>
          </>
        )}
      </div>

      <div className="swipe-actions">
        <button className="action-btn undo" onClick={() => {}} title="Отменить">
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2" strokeLinecap="round" strokeLinejoin="round">
            <path d="M3 12a9 9 0 1 0 9-9 9.75 9.75 0 0 0-6.74 2.74L3 8" />
            <path d="M3 3v5h5" />
          </svg>
        </button>
        <button className="action-btn dislike" onClick={() => handleSwipe('dislike')}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M10 15L3 8M10 15L10 15C10 15 10 15 10 15L18 15C19.5 15 21 13.5 21 12L21 8C21 6.5 19.5 5 18 5L14 5L14 5L10 5L10 15Z" />
            <line x1="3" y1="3" x2="21" y2="21" strokeWidth="2.5" />
          </svg>
        </button>
        <button className="action-btn like" onClick={() => handleSwipe('like')}>
          <svg viewBox="0 0 24 24" fill="none" stroke="currentColor" strokeWidth="2.5" strokeLinecap="round" strokeLinejoin="round">
            <path d="M20.84 4.61a5.5 5.5 0 0 0-7.78 0L12 5.67l-1.06-1.06a5.5 5.5 0 0 0-7.78 7.78l1.06 1.06L12 21.23l7.78-7.78 1.06-1.06a5.5 5.5 0 0 0 0-7.78z" />
          </svg>
        </button>
      </div>
    </div>
  );
}

function UserCard({ item }: { item: FeedItem }) {
  return (
    <>
      {item.photo ? (
        <img className="card-photo" src={item.photo} alt={item.name} />
      ) : (
        <div className="card-placeholder">{item.name?.charAt(0) || '?'}</div>
      )}
      <div className="card-info">
        <div className="card-name-row">
          <span className="card-name">{item.name}</span>
          {item.age && <span className="card-age">{item.age}</span>}
        </div>
        <div className="card-city">📍 {item.city}</div>
        {item.bio && <div className="card-bio">{item.bio}</div>}
        <div className="card-tags">
          {item.gender && <span className="tag">{item.gender === 'female' ? 'Женский' : item.gender === 'male' ? 'Мужской' : 'Другой'}</span>}
          <span className="tag green">📍 {item.city}</span>
        </div>
        <div className="card-compatibility">
          <div className="compat-bar">
            <div className="compat-fill" style={{ width: `${item.compatibility}%` }} />
          </div>
          <span className="compat-text">{Math.round(item.compatibility)}%</span>
        </div>
      </div>
    </>
  );
}

function ListingCard({ item }: { item: FeedItem }) {
  return (
    <>
      {item.photo ? (
        <img className="card-photo" src={item.photo} alt={item.name} />
      ) : (
        <div className="card-placeholder">🏠</div>
      )}
      <div className="card-listing-info">
        <div className="card-listing-type">{item.listing_type}</div>
        <div className="card-listing-name">{item.name}</div>
        <div className="card-listing-address">📍 {item.city}{item.district ? `, ${item.district}` : ''}</div>
        {item.budget_min && item.budget_max && (
          <div className="card-budget">
            {item.budget_min.toLocaleString()} — {item.budget_max.toLocaleString()} ₽/мес
          </div>
        )}
        {item.description && <div className="card-listing-desc">{item.description}</div>}
        <div className="card-compatibility" style={{ marginTop: 12 }}>
          <div className="compat-bar">
            <div className="compat-fill" style={{ width: `${item.compatibility}%` }} />
          </div>
          <span className="compat-text">{Math.round(item.compatibility)}%</span>
        </div>
      </div>
    </>
  );
}
