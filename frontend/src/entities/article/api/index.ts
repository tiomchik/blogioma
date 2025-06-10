const loadArticlesOrderedByField = async (
  field: string,
  amount?: number
): Promise<Response> => {
  const response = await fetch(
    `${import.meta.env.VITE_API_URL}/articles/?order_by=${field}&page_size=${amount ? amount : ""}`
  );
  return response.json();
};

export { loadArticlesOrderedByField };
