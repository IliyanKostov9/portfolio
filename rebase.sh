#!/bin/bash

# Loop until the rebase is finished
while true; do
    # Stage all changes
    git add .

    # Attempt to continue the rebase
    if git rebase --continue; then
        echo "Rebase continued successfully."
        break  # Exit the loop if the rebase was successful
    else
        echo "Rebase encountered a conflict. Please resolve conflicts."
        echo "Continuing the loop..."
        # Wait for user to resolve conflicts before next iteration
        read -p "Press [Enter] when conflicts are resolved and you want to continue..."
    fi
done
