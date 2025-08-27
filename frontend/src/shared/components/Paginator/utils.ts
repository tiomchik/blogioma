const hasManyPagesBeforeCurrent = (page: number) => {
  return page - 3 > 1;
};

const hasManyPagesAfterCurrent = (page: number, pageAmount: number) => {
  return page + 3 < pageAmount;
};

export { hasManyPagesBeforeCurrent, hasManyPagesAfterCurrent };
