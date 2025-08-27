const generateListOfPagesAroundCurrent = (
  currentPage: number,
  pageAmount: number
) => {
  const pages = [
    currentPage - 2,
    currentPage - 1,
    currentPage,
    currentPage + 1,
    currentPage + 2,
  ].filter((page) => page > 1 && page < pageAmount);
  return pages;
};

export { generateListOfPagesAroundCurrent };
