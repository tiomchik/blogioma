import { describe, expect, test, vi } from "vitest";
import {
  getSortingFieldByCriteria,
  loadArticlesSortedByCriteria,
  getArticles,
} from ".";
import { ARTICLES_URL } from "./constants";
import axios from "axios";

vi.mock("axios", () => {
  return {
    default: {
      get: vi.fn(() => ({ data: expectedData })),
    },
  };
});

const expectedData = "data";

const sortingCriteria = "popular";
const sortingField = getSortingFieldByCriteria(sortingCriteria);
const amount = 3;
const page = 2;
const expectedAxiosParams = { order_by: sortingField, page_size: amount, page };

const mockAxiosGet = vi.mocked(axios.get);

describe("loadArticlesSortedByCriteria", () => {
  test("axios.get was called with correct URL and sorting field", async () => {
    const data = await loadArticlesSortedByCriteria(sortingCriteria);
    expect(mockAxiosGet).toBeCalledWith(ARTICLES_URL, {
      params: { order_by: sortingField },
    });
    expect(data).toEqual(expectedData);
  });

  test("axios.get was called with page size", async () => {
    const data = await loadArticlesSortedByCriteria(sortingCriteria, {
      amount,
    });
    expect(mockAxiosGet).toBeCalledWith(ARTICLES_URL, {
      params: { order_by: sortingField, page_size: amount },
    });
    expect(data).toEqual(expectedData);
  });

  test("axios.get was called with page size and page", async () => {
    const data = await loadArticlesSortedByCriteria(sortingCriteria, {
      amount,
      page,
    });
    expect(mockAxiosGet).toBeCalledWith(ARTICLES_URL, {
      params: expectedAxiosParams,
    });
    expect(data).toEqual(expectedData);
  });
});

describe("getSortingFieldByCriteria", () => {
  test("returns correct sorting field", () => {
    expect(getSortingFieldByCriteria("popular")).toBe("-viewings");
    expect(getSortingFieldByCriteria("latest")).toBe("-pub_date");
  });

  test("error was thrown if invalid criteria is passed", () => {
    const invalidCriteria = "invalid" as any;
    expect(() => getSortingFieldByCriteria(invalidCriteria)).toThrow(
      "Invalid sorting criteria"
    );
  });
});

describe("getArticles", () => {
  test("axios.get was called with valid url and default params", async () => {
    const data = await getArticles(ARTICLES_URL);
    expect(mockAxiosGet).toBeCalledWith(ARTICLES_URL, {
      params: { order_by: getSortingFieldByCriteria("latest") },
    });
    expect(data).toBe(expectedData);
  });

  test("axios.get was called with correct params", async () => {
    await getArticles(ARTICLES_URL, { sortingCriteria, amount, page });
    expect(mockAxiosGet).toBeCalledWith(ARTICLES_URL, {
      params: expectedAxiosParams,
    });
  });
});
