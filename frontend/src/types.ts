export interface Establishment {
  id: number;
  uuid: string;
  name: string;
  permit_name?: string;
  address: string;
  city: string;
  state: string;
  zip: string;
  created_at: string;
  updated_at: string;
}

export interface Closure {
  id: number;
  uuid: string;
  establishment_id: number;
  closed_on: string;
  reopened_on?: string;
  reason?: string;
  result?: string;
  created_at: string;
  updated_at: string;
  establishment: Establishment;
}
