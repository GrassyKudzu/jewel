use std::env;

fn defang_url(url: &str) -> String {
    let defanged_url = if url.contains("[.]") {
        url.replace("[.]", ".")
    } else if url.matches('.').count() == 1 {
        url.replace(".", "[.]")
    } else if url.matches('.').count() == 2 {
        let first_period_index = url.find('.').unwrap();
        let second_period_index = url.rfind('.').unwrap();
        url[..first_period_index].to_string()
            + "[." + &url[first_period_index + 1..second_period_index] + ".]"
            + &url[second_period_index + 1..]
    } else {
        url.to_string()
    };

    if defanged_url.starts_with("http://") {
        defanged_url.replace("http://", "hxxp://")
    } else if defanged_url.starts_with("https://") {
        defanged_url.replace("https://", "hxxps://")
    } else if defanged_url.starts_with("ftp://") {
        defanged_url.replace("ftp://", "fxp://")
    } else if defanged_url.starts_with("file://") {
        defanged_url.replace("file://", "fxxe://")
    } else {
        defanged_url.to_string()
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 3 {
        println!("Usage: ./script <defang/restore> <URL>");
        return;
    }

    let action = &args[1];
    let normal_url = &args[2];

    if action == "defang" {
        let defanged_url = defang_url(normal_url);
        println!("DEFANGED URL: {}", defanged_url);
    } else if action == "restore" {
        let restored_url = defang_url(normal_url);
        println!("RESTORED URL: {}", restored_url);
    } else {
        println!("Invalid action. Use 'defang' or 'restore'.");
    }
}
