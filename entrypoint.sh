#!/bin/bash
cat << EOF
Для запуска тестов введите: pytest
Для запуска тестов с покрытием введите: pytest --cov=src/ --cov-report=term
Для просмотра инструкции к программе введите: python -m src instruct
Для выполнения какой-либо другой команды программы введите ее согласно инструкции, например:
python -m src read example_1.jsonl --contains проект
EOF

while true; do
  read -p '> ' cmd
  if [[ "\$cmd" == "exit" || "\$cmd" == "quit" ]]; then
    break
  fi
  if [[ -n "\$cmd" ]]; then
    eval "\$cmd"
  fi
done