import { describe, expect, test, vi } from "vitest";
import { loadArticlesOrderedByField } from ".";
import axios from "axios";

vi.mock("axios", () => {
  return {
    default: {
      get: vi.fn(() => ({ data: {} })),
    },
  };
});

const mockedAxiosGet = vi.mocked(axios.get);

describe("loadArticlesOrderedByField", () => {
  test("axios.get was called with correct URL without page size", async () => {
    await loadArticlesOrderedByField("heading");
    expect(mockedAxiosGet).toBeCalledWith(
      `${import.meta.env.VITE_API_URL}/articles/?order_by=heading&page_size=`
    );
  });

  test("axios.get was called with correct URL with page size", async () => {
    await loadArticlesOrderedByField("heading", 3);
    expect(mockedAxiosGet).toBeCalledWith(
      `${import.meta.env.VITE_API_URL}/articles/?order_by=heading&page_size=3`
    );
  });
});
