(defun fib(n)
  (if (<= n 1)
      n
     (+ (fib(- n 1)) (fib (- n 2)))))

(defun print-fib (n)
   (dotimes (i n)
     (format t "~a " (fib i))))
