import axios from "axios";

const loadArticlesOrderedByField = async (
  field: string,
  amount?: number
): Promise<Response> => {
  const response = await axios.get(
    `${import.meta.env.VITE_API_URL}/articles/?order_by=${field}&page_size=${amount ? amount : ""}`
  );
  return response.data;
};

export { loadArticlesOrderedByField };
