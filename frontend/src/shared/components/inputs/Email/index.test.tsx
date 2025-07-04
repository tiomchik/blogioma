import { beforeEach, test } from "vitest";
import EmailInput, { EMAIL_FIELD_LABEL } from "./";
import {
  expectErrorMessage,
  pasteIntoFieldByLabelText,
  renderInputWithFormProvider,
} from "@/tests/utils";
import userEvent from "@testing-library/user-event";

beforeEach(() => {
  renderInputWithFormProvider(<EmailInput />);
});

test("should display an error for invalid email", async () => {
  pasteIntoFieldByLabelText(EMAIL_FIELD_LABEL, "invalid@email");
  await userEvent.tab();
  expectErrorMessage(/Email is not valid/);
});
