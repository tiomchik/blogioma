const USERNAME_ERROR_TEXT = "Username cannot be empty";

const generateUserArticlesUrl = (username: string) => {
  if (!username) {
    throw new Error(USERNAME_ERROR_TEXT);
  }
  return `${import.meta.env.VITE_API_URL}/users/${encodeURIComponent(username)}/articles/`;
};

export { generateUserArticlesUrl, USERNAME_ERROR_TEXT };
