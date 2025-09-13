import { io } from 'socket.io-client';

export const socket = io(
  import.meta.env.NEXT_PUBLIC_WS_URL || 'ws://localhost:3000'
);
