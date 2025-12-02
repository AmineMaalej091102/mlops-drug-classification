# main.py
import argparse
from model_pipeline import (
    prepare_data,
    train_model,
    evaluate_model,
    save_model,
    load_model,
)


def main():
    parser = argparse.ArgumentParser(
        description="Pipeline ML - Classification de Medicaments (Naive Bayes)"
    )
    parser.add_argument("data_path", type=str, help="Chemin vers drug200.csv")
    parser.add_argument("--train", action="store_true", help="Entrainer le modele")
    parser.add_argument("--evaluate", action="store_true", help="Evaluer le modele")
    parser.add_argument("--load", type=str, help="Chemin du modele sauvegarde")

    args = parser.parse_args()

    if args.load:
        model, _ = load_model(args.load)
        _, X_test, _, y_test, _ = prepare_data(args.data_path)
        evaluate_model(model, X_test, y_test)

    elif args.train or args.evaluate:
        X_train, X_test, y_train, y_test, encoders = prepare_data(args.data_path)
        model = train_model(X_train, y_train)

        if args.evaluate:
            evaluate_model(model, X_test, y_test)

        if args.train:
            save_model(model, encoders, filename="nb_drug_model.joblib")

    else:
        parser.print_help()


if __name__ == "__main__":
    main()
