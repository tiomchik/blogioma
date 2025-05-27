export const truncateWithEllipsis = (text: string, length: number) => {
  if (text.length > length) {
    return text.slice(0, length) + "...";
  } else {
    return text;
  }
};

export const formatDate = (date: Date): string => {
  const month = date.toLocaleString("eng", { month: "long" });
  const day = date.getDate();
  const year = date.getFullYear();
  const hours = date.getHours();
  const minutes = date.getMinutes();
  return `${month} ${day}, ${year}, ${hours}:${minutes} a.m.`;
};
