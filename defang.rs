use std::env;
use std::fs;

fn defang_url(url: &str) -> String {
    let defanged_url = url.replace("[.]", ".");
    if defanged_url.matches('.').count() == 2 {
        let first_period_index = defanged_url.find('.').unwrap();
        let second_period_index = defanged_url.rfind('.').unwrap();
        return defanged_url[..first_period_index].to_string()
            + "[."
            + &defanged_url[first_period_index + 1..second_period_index]
            + ".]"
            + &defanged_url[second_period_index + 1..];
    } else if defanged_url.matches('.').count() == 1 {
        return defanged_url.replace(".", "[.]");
    }
    defanged_url.to_string()
}

fn modify_protocol(url: &str) -> String {
    if url.starts_with("http://") {
        return url.replace("http://", "hxxp://");
    } else if url.starts_with("https://") {
        return url.replace("https://", "hxxps://");
    } else if url.starts_with("ftp://") {
        return url.replace("ftp://", "fxp://");
    } else if url.starts_with("file://") {
        return url.replace("file://", "fxxe://");
    }
    url.to_string()
}

fn process_urls(
    urls: Vec<String>,
    action: &str,
    modify_protocol_option: bool,
    output_file: Option<&str>,
) {
    let mut modified_urls = Vec::new();

    for url in urls {
        let modified_url = if modify_protocol_option {
            modify_protocol(&url)
        } else {
            url
        };

        let defanged_url = match action {
            "defang" => defang_url(&modified_url),
            "restore" => defang_url(&modified_url),
            _ => {
                println!("Invalid action. Use 'defang' or 'restore'.");
                return;
            }
        };

        modified_urls.push(defanged_url);
    }

    if let Some(output_file_path) = output_file {
        fs::write(output_file_path, modified_urls.join("\n"))
            .expect("Failed to write output file.");
    } else {
        println!("Modified URLs:");
        for url in modified_urls {
            println!("{}", url);
        }
    }
}

fn main() {
    let args: Vec<String> = env::args().collect();

    let mut input_file = String::new();
    let mut output_file = None;
    let mut action = String::new();
    let mut modify_protocol_option = false;

    let mut i = 1;
    while i < args.len() {
        match args[i].as_str() {
            "-i" | "--inputFile" => {
                i += 1;
                input_file = args[i].clone();
            }
            "-o" | "--outputFile" => {
                i += 1;
                output_file = Some(args[i].as_str());
            }
            "-a" | "--action" => {
                i += 1;
                action = args[i].clone();
            }
            "--modifyProtocol" => {
                modify_protocol_option = true;
            }
            _ => {}
        }
        i += 1;
    }

    if input_file.is_empty() || action.is_empty() {
        println!("Usage: ./script -i <input_file> -o <output_file> -a <action> [--modifyProtocol]");
        return;
    }

    let content = match fs::read_to_string(input_file) {
        Ok(content) => content,
        Err(_) => {
            println!("Input file not found.");
            return;
        }
    };

    let urls: Vec<String> = content.lines().map(|s| s.trim().to_string()).collect();
    process_urls(
        urls,
        &action,
        modify_protocol_option,
        output_file.as_deref(),
    );
}
