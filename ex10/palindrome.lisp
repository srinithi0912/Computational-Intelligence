(defun palindrome-number (n)
  (let ((original n)
        (rev 0))
    (loop while (> n 0) do
      (setq rev (+ (* rev 10) (mod n 10)))
      (setq n (floor n 10)))
    (= original rev)))

(defun palindrome-input ()
  (format t "Enter number: ")
  (let ((n (read)))
    (if (palindrome-number n)
        (format t "palindrome")
        (format t "not a palindrome"))))
