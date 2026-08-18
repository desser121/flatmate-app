export interface User {
  id: string;
  phone: string;
  name: string;
  birth_date: string;
  gender: string;
  city: string;
  bio: string;
  role_seeker: boolean;
  role_roommate: boolean;
  role_landlord: boolean;
  photos: UserPhoto[];
  age: number | null;
  profile_complete: boolean;
  created_at: string;
  updated_at: string;
}

export interface UserPhoto {
  id: string;
  image: string;
  order: number;
  is_primary: boolean;
}

export interface Preference {
  city: string;
  district: string;
  budget_min: number;
  budget_max: number;
  gender_pref: string;
  age_min: number;
  age_max: number;
  smoking: string;
  pets: string;
  schedule: string;
  rental_period: string;
}

export interface Listing {
  id: string;
  user: string;
  author_name: string;
  listing_type: string;
  property_type: string;
  city: string;
  district: string;
  address: string;
  budget_min: number;
  budget_max: number;
  description: string;
  is_active: boolean;
  photos: ListingPhoto[];
  created_at: string;
}

export interface ListingPhoto {
  id: string;
  image: string;
  order: number;
}

export interface FeedItem {
  type: 'user' | 'listing';
  id: string;
  name: string;
  age?: number;
  gender?: string;
  city: string;
  bio?: string;
  photo: string;
  compatibility: number;
  listing_type?: string;
  property_type?: string;
  budget_min?: number;
  budget_max?: number;
  description?: string;
  district?: string;
  address?: string;
}

export interface Match {
  id: string;
  other_user: User;
  listing: string | null;
  created_at: string;
}

export interface Conversation {
  id: string;
  match: string;
  other_user: User;
  last_message: {
    content: string;
    message_type: string;
    created_at: string;
  } | null;
  unread_count: number;
  last_message_at: string;
}

export interface Message {
  id: string;
  author: string;
  author_name: string;
  content: string;
  message_type: string;
  attachment_url: string;
  is_read: boolean;
  created_at: string;
}
