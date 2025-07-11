import { describe, expect, test, vi } from "vitest";
import {
  ARTICLES_BASE_URL,
  getSortingFieldByCriteria,
  loadArticlesSortedByCriteria,
} from ".";
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
  test("axios.get was called with correct URL without page size", async () => {
    await loadArticlesSortedByCriteria("popular");
    expect(mockedAxiosGet).toBeCalledWith(
      `${ARTICLES_BASE_URL}/?order_by=-viewings&page_size=`
    );
  });

  test("axios.get was called with correct URL with page size", async () => {
    await loadArticlesSortedByCriteria("popular", 3);
    expect(mockedAxiosGet).toBeCalledWith(
      `${ARTICLES_BASE_URL}/?order_by=-viewings&page_size=3`
    );
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
