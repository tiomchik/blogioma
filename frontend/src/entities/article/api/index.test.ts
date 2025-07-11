import { describe, expect, test, vi } from "vitest";
import { ARTICLES_BASE_URL, loadArticlesSortedByCriteria } from ".";
import axios from "axios";

vi.mock("axios", () => {
  return {
    default: {
      get: vi.fn(() => ({ data: {} })),
    },
  };
});

const mockedAxiosGet = vi.mocked(axios.get);

describe("loadArticlesSortedByCriteria", () => {
  test("axios.get was called with correct URL", async () => {
    await loadArticlesSortedByCriteria("popular");
    expect(mockedAxiosGet).toBeCalledWith(
      `${ARTICLES_BASE_URL}/?order_by=-viewings&page_size=`
    );

    await loadArticlesSortedByCriteria("latest");
    expect(mockedAxiosGet).toBeCalledWith(
      `${ARTICLES_BASE_URL}/?order_by=-pub_date&page_size=`
    );
  });

  test("axios.get was called with correct URL with page size", async () => {
    await loadArticlesSortedByCriteria("popular", 3);
    expect(mockedAxiosGet).toBeCalledWith(
      `${ARTICLES_BASE_URL}/?order_by=-viewings&page_size=3`
    );
  });

  test("error was thrown if invalid criteria is passed", async () => {
    const invalidCriteria = "invalid" as any;
    expect(loadArticlesSortedByCriteria(invalidCriteria)).rejects.toThrow(
      "Invalid sorting criteria"
    );
  });
});
