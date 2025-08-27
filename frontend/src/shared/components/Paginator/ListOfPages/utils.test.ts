import { describe, expect, test } from "vitest";
import { generateListOfPagesAroundCurrent } from "./utils";

describe("generateListOfPagesAroundCurrent", () => {
  test("returns next two numbers if current page is 1", () => {
    const expectedPages = [2, 3];
    const pages = generateListOfPagesAroundCurrent(1, 10);
    expect(pages).toEqual(expectedPages);
  });

  test("returns next two numbers if current page is 2", () => {
    const expectedPages = [2, 3, 4];
    const pages = generateListOfPagesAroundCurrent(2, 10);
    expect(pages).toEqual(expectedPages);
  });

  test("returns previous one number and next two if current page is 3", () => {
    const expectedPages = [2, 3, 4, 5];
    const pages = generateListOfPagesAroundCurrent(3, 10);
    expect(pages).toEqual(expectedPages);
  });

  test("returns previous two numbers and next two", () => {
    const expectedPages = [3, 4, 5, 6, 7];
    const pages = generateListOfPagesAroundCurrent(5, 10);
    expect(pages).toEqual(expectedPages);
  });

  test("returns previous two numbers and next one when close to but not at the end", () => {
    const expectedPages = [6, 7, 8, 9];
    const pages = generateListOfPagesAroundCurrent(8, 10);
    expect(pages).toEqual(expectedPages);
  });

  test("returns previous two numbers if current page is last", () => {
    const expectedPages = [8, 9];
    const pages = generateListOfPagesAroundCurrent(10, 10);
    expect(pages).toEqual(expectedPages);
  });
});
