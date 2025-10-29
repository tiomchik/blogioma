export const truncateWithEllipsis = (text: string, length: number): string => {
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
  const hours = date.getHours().toString().padStart(2, "0");
  const minutes = date.getMinutes().toString().padStart(2, "0");

  const baseFormat = `${month} ${day}, ${hours}:${minutes}`;

  return isCurrentYear(year) ? baseFormat : `${year}, ${baseFormat}`;
};

const isCurrentYear = (year: number) => {
  const currentYear = new Date().getFullYear();
  return year == currentYear;
};
