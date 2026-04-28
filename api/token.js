import { AccessToken } from "livekit-server-sdk";

export default function handler(req, res) {
  const token = new AccessToken(
    process.env.LIVEKIT_API_KEY,
    process.env.LIVEKIT_API_SECRET,
    { identity: "user-" + Date.now() }
  );
  token.addGrant({ roomJoin: true, room: "agent-room" });
  res.json({
    token: token.toJwt(),
    url: process.env.LIVEKIT_URL,
  });
}
