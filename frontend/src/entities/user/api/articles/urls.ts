const USERNAME_ERROR_TEXT = "Username cannot be empty";
const USERS_URL = `${import.meta.env.VITE_API_URL}/users`;

const generateUserArticlesUrl = (username: string) => {
  if (!username) throw new Error(USERNAME_ERROR_TEXT);
  return `${USERS_URL}/${encodeURIComponent(username)}/articles/`;
};

export { generateUserArticlesUrl, USERNAME_ERROR_TEXT, USERS_URL };
